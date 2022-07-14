from otakudesu import OtakuDesu
from utilities import jsonify
otak = OtakuDesu()
class SearchOtakudesu(OtakuDesu):
    def __init__(self, query) -> None:
        super().__init__()
        self.result = self.toJson(self.search(query).result)
    def toJson(self, obj):
        if type(obj).__name__ == 'SimpleNamespace':
            return self.toJson(obj.__dict__)
        elif type(obj).__name__ == 'dict':
            return {i: self.toJson(obj[i]) for i in obj.keys()}
        elif type(obj).__name__ == 'list':
            return [self.toJson(i) for i in obj]
        else:
            return obj


def Otakudesu(request):
    if not request.GET.get("query"):return jsonify({"status": 400, "msg": "Parameter query jangan kosong"}, 400)
    try:
        quer = request.GET.get("query")
        return jsonify(SearchOtakudesu(query=quer).result, 200)
    except Exception as e:
        print(e)
        return jsonify({"status": 409, "msg": "Anime tidak ditemukan"}, 409)