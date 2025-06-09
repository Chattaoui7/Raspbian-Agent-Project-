libcamera-vid -t 0 --width 800 --height 400 --framerate 24 --vflip --nopreview -o - | cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8160}' :demux=h264
