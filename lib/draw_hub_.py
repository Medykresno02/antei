from utilities.file_ import makefile
from utilities import get_file_json
from utilities import jsonify
from phlogo import generate
from io import BytesIO
def phgenerate(request):
    x = request.GET.get("x", " ")[:16]
    y = request.GET.get("y", " ")[:16]
    b = BytesIO()
    generate(x, y).save(b, format="png")
    file=get_file_json(makefile("-".join([x,y]), b.getvalue()), request)
    return jsonify(file, 200)