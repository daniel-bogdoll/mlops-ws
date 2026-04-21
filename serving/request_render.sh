curl https://mlops-ws-intern-1.onrender.com/invocations \
  -H "Content-Type:application/json" \
  --data '{
    "inputs": [
      {
        "totalAmount": 100.0,
        "customerType_new": 1,
        "orderedBooks": 4
      }
    ]
  }'