<?php

$images = array();
$files = scandir('.', SCANDIR_SORT_DESCENDING);
foreach ($files as $file) {
  if (preg_match('@\.jpg$@', $file)) {
    array_push($images, $file);
  }
}


?>
<!doctype html>
<html>
    <head>
        <title>Alice's Spooky Party</title>
        <meta http-equiv="refresh" content="10"/>
        <style>
          div.photo {
            width: 600px;
            text-align: center;
            margin: 0px auto 40px;
          }
          div.photo img {
              width: 600px;
              height: 400px;
          }
        </style>
    </head>
    <body>
      <?php
        foreach($images as $image) {
          echo <<<HTML
        <div class="photo">
          <img src="{$image}" />
          <span>$image</span>
        </div>
HTML;
        }
      ?>
      <pre><?php print_r($images); ?></pre>
    </body>

</html>
