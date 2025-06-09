import os

def split_file(data, chunk_size):
    """
    Büyük bir veriyi (data) belirli büyüklükteki parçalara (chunk) böler.
    Mesela dosya çok büyükse, daha küçük parçalara ayırarak işleyebiliriz.
    chunk_size: parçaların byte cinsinden büyüklüğü.
    """
    return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

def join_chunks(chunks):
    """
    Parçalanmış byte dizilerini tekrar birleştirir.
    Yani, split_file ile bölünmüş veriyi eski haline getirir.
    """
    return b''.join(chunks)

def get_file_size(path):
    """
    Verilen dosya yolundaki dosyanın byte cinsinden boyutunu döner.
    """
    return os.path.getsize(path)
