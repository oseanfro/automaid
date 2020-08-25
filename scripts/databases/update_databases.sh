 #!/bin/bash
 
 rsync -avz --delete --exclude="*update_databases*" ./ root@164.132.96.221:/root/web/databases/
