git pull
docker build . -t utda/sim_utda:1.0
docker stop sim_utda
docker rm sim_utda
docker run --name sim_utda -itd -p 8022:5001 utda/sim_utda:1.0
