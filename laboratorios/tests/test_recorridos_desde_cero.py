import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("recorridos", ROOT / "recorridos_desde_cero.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)

def test_bfs():
    assert lab.bfs_camino(lab.GRAFO, "A", "D") == ["A", "B", "D"]

def test_dfs():
    assert lab.dfs_camino(lab.GRAFO, "A", "D") == ["A", "C", "E", "D"]

def test_dijkstra():
    fewer_hops, lower_cost, cost = lab.comparar_caminos()
    assert fewer_hops == ["A", "B", "D"]
    assert lower_cost == ["A", "C", "E", "D"]
    assert cost == 3

def test_no_path():
    assert lab.bfs_camino({"A": [], "D": []}, "A", "D") is None
