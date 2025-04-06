from pymongo import MongoClient

MONGO_URI = "mongodb://cosmosteste1:VAkllNZUbPVfE2fB2BsPWLTDoS6UkcOfJIUjkPWaJg56rrZPZQjUnR5IBIDvzk6pKQFHOx4AKl3CACDbSIwWdA==@cosmosteste1.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@cosmosteste1@"

client = MongoClient(MONGO_URI)



