if [[ $# -ne 1 ]]; then
    echo "Requires exactly 1 argument. Tag"
    exit 1
fi

docker build -t kentonvp/surfsup-bot:$1 .
docker push kentonvp/surfsup-bot:$1