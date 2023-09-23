from flask import Flask
from secrets import randbelow
from datetime import datetime
from collections import defaultdict
  
  
app = Flask(__name__)



class post():
    id: int
    key: str
    timestamp: str
    msg: str

    def __init__(self, _id, _key, _msg) :
        self.id = _id
        self.key = _key
        self.msg = _msg
        self.timestamp = datetime.utcnow().isoformat()
        
    
    def __repr__(self) :
        return f'post({self.id!r}, {self.key!r}, {self.timestamp!r}, {self.msg!r})'

def get_output_json(_post: post, include_key : bool):
    output = {}
    output['id'] = post.id
    if include_key : 
        output['key'] = post.key
    output['timestamp'] = post.timestamp
    output['msg'] = post.msg
    return jsonify(output)


posts_dict = {}
posts_count = 0
@app.route('/post', methods=['POST'])
def create_post():
    global posts_count, posts_dict

    # validate the content-type
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json') :
        input_json = request.get_json()
    else:
        return jsonify({'err': 'Incompatible Content-Type'}), 400

    # validate and check if msg field is present in the input
    if 'msg' in input_json :
        input_msg = input_json['msg']
    else :
        return jsonify({'err': 'Missing msg field'}), 400
    
    # assign global posts_count as id and increment it 
    _id = len(posts_count)
    posts_count += 1
    
    # create a unique key using secrets
    _key = secrets.token_hex(16)

    # assign input_msg received in the request
    _msg = input_msg
    
    # create a post object 
    _post = post(_id, _key, _msg)

    # insert the created post into posts_dict
    posts_dict[_id] = _post

    output_json = get_output_json(_post, true)
    return output_json, 201

@app.route('/post/<int:_id>', methods=['GET'])
def get_post(_id):
    global posts_dict
    if _id not in posts_dict:
        return jsonify({'err': 'Post with given id not found'}), 404
    
    _post = posts_dict[_id]
    output_json = get_output_json_without_key(_post, false)
    return jsonify(result), 200


@app.route('/post/<int:_id>/delete/<string:_key>', methods=['DELETE'])
def delete_post(_id, _key):
    global posts_dict
    if _id not in posts_dict:
        return jsonify({'err': 'Post with given id not found'}), 404
    
    _post = posts_dict[_id]
    if _post.key != _key:
        return jsonify({'err': 'Delete forbidden due to key mismatch'}), 403
    
    del posts_dict[_id]
    output_json = get_output_json(_post, true)
    return output_json, 200




