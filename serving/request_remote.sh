curl http://34.32.50.125:5000/invocations \
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