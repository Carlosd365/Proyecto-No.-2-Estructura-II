
FNV_OFFSET_BASIS_32 = 2166136261
FNV_PRIME_32 = 16777619
MASK_32 = 0xFFFFFFFF

def fnv1_32(data_bytes: bytes) -> int:
    h = FNV_OFFSET_BASIS_32
    for b in data_bytes:
        h = (h * FNV_PRIME_32) & MASK_32
        h ^= b
    return h

def calcular_hash_archivo(ruta: str) -> str:
    with open(ruta, "rb") as f:
        data = f.read()
    h = fnv1_32(data)
    return str(h)  
