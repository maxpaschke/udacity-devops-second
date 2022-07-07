from app import scale, home, predict

def test_title():
    assert "<h3>Sklearn Prediction Home</h3>" == home()
