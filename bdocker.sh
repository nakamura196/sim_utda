docker build . -t utda/sim_utda:1.0
docker run -itd -p 8022:5001 utda/sim_utda:1.0
