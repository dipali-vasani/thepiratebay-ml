import json
import sys

from flask import Flask, request, Response,jsonify
from cortex_client import OutputMessage



import pandas as pd
import os
import turicreate





ratings = pd.read_csv('data.csv', sep=',', header=0)
ratings['user']= ratings['user_name'].astype('category').cat.codes

def getUserId(name):
    df = ratings[ratings['user_name']==name]['user'].max()
    if(df>=0):
        return df
    else :
        return -1


train_data = turicreate.SFrame(ratings)
#Training the model
item_sim_model = turicreate.item_similarity_recommender.create(train_data, user_id='user', item_id='item', target='rating', similarity_type='cosine')

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def health():
    return Response(status=200,
                    response=json.dumps({'message': 'success'}),
                    mimetype='application/json')


@app.route('/invoke', methods=['POST'])
def invokeJob():
    params = json.loads(request.data)
    req = params.get('payload').get('test_data')
    token = params.get('token')
    user=  req.get('user')
    try:
        #Making recommendations
        userid = int(getUserId(user))
        #app.logger.error("userid "+userid)
        item_sim_recomm = item_sim_model.recommend(users=[userid],k=5)
        resp = {"items":list(item_sim_recomm['item'])}
        return Response(status=200,
                        response=json.dumps(OutputMessage.create().with_payload(
                            resp).to_params()),
                        mimetype='application/json')
    except Exception:
        ex = sys.exc_info()
        return Response(status=500,
                        response=json.dumps(OutputMessage.create().with_payload(
                            str(ex)).to_params()),
                        mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, threaded=True)
