Write-Host "----------- Deleting old pod -----------" -ForegroundColor Yellow
$delete_pod = "kubectl delete pod keci-pod"
Invoke-Expression $delete_pod
Write-Host "----------- Old pod deleted -----------" -ForegroundColor Green

Write-Host "----------- Building new image -----------" -ForegroundColor Yellow
$build_image = "docker build -t keci ."
Invoke-Expression $build_image
Write-Host "----------- Image built -----------" -ForegroundColor Green

Write-Host "----------- Tagging new image -----------" -ForegroundColor Yellow
$tag_image = "docker tag keci:latest localhost:5000/keci:latest"
Invoke-Expression $tag_image
Write-Host "----------- Image tagged -----------" -ForegroundColor Green

Write-Host "----------- Pushing image to repo -----------" -ForegroundColor Yellow
$push_to_repo = "docker push  localhost:5000/keci:latest"
Invoke-Expression $push_to_repo
Write-Host "----------- Image pushed -----------" -ForegroundColor Green

Write-Host "----------- Creating new pod -----------" -ForegroundColor Yellow
$create_pod = "kubectl create -f .\k8s\keci-pod.yaml"
Invoke-Expression $create_pod
Write-Host "----------- Pod created -----------" -ForegroundColor Green
