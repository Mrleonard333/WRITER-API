<?php
function Request_Code()
{                                              # v Will get the function's first argument
    $Description = array("description" => func_get_arg(0));

    $Request = json_encode($Description); # < Will store the data in json format
    $Context = stream_context_create( # < Will create a context for the request
        array(
            'http' => array(
                'method' => 'POST',
                'header' => ['Content-Type: application/json', 'Content-length' . strlen($Request)],
                'content' => $Request # < The json content
    )));
                            # v Will request the DataBase scripts
    $Content = json_decode(file_get_contents("http://localhost:5000/get_code", false, $Context));
    echo $Content->Results->code; # < Will run the code
};
?>

<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
</head>

<style>
<?php
    Request_Code("Will change the background")
?>
</style>

<body style="font-family: Arial">
    <h1>[Writer test page]</h1>

    <?php 
    Request_Code("php icon")
    ?>
</body>
</html>