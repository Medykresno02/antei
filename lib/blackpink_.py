from utilities.file_ import makefile
from utilities import get_file_json
from io import BytesIO
from utilities import jsonify
from blackpink import blackpink as blackping
def blackpink(request):
    if request.GET.get("text"):
        buf=BytesIO()
        blackping(request.GET["text"][:20]).save(buf, format="png")
        file=get_file_json(makefile(f"{request.GET['text']}",buf.getvalue()), request)
        return jsonify(file, 200)
    else:
        return jsonify({'status': 400, 'msg': 'Parameter text jangan kosong'}, 400)