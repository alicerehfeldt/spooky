<?php

$images = new Array();
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
    </body>

</html>
