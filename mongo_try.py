import pymongo
print(pymongo.version)
if __name__=="__main__":
    client=pymongo.MongoClient("mongodb+srv://workingyatri:QF0jmjKOfREtICoS@cluster1.fqv7v2j.mongodb.net/")
    print(client)
    db=client['Status_Table']
    collection=db['Status']
    one=collection.find_one({'_id':1},{'status':1,'Emstat':1,'_id':0})
    print(one)
    prev={"status":0}
    next={"$set":{"status":1}}
    collection.update_one(prev,next)