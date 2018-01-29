import pytest
from tax_calc import trades

@pytest.fixture
def tr():
	tr = trades()
	def cleanup_tr():
		tr.clear()

	return tr

def test_load_csv(tr):
	tr.load_csv('filepath/eth_gdax_account.csv')
	assert 0 < len(tr.trans)

# run by typing 'pytest' in terminal in the project directory