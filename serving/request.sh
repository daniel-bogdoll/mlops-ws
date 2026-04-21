# sh serving/requests.sh

curl http://127.0.0.1:5000/invocations \
  -H "Content-Type:application/json" \
  --data '{
    "inputs": [
      {
        "transactionId": 9534310106,
        "basket": [4, 3, 4],
        "totalAmount": 366,
        "customerType": "new"
      }
    ]
  }'