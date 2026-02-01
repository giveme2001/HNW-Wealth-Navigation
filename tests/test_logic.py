import sys
import os

# core 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.calc_engine import InheritanceTaxCalculator
from decimal import Decimal

def test_calc():
    calc = InheritanceTaxCalculator()
    
    # TC 1: 자산 10억, 배우자 있음, 자녀 있음 (일괄공제 5억 + 배우자공제 5억 = 10억 공제) -> 세금 0
    res1 = calc.calculate_inheritance_tax(1000000000, 0, True, 2)
    print(f"TC1 (10억): {res1['tax_amount']} (Expect: 0)")
    assert res1['tax_amount'] == 0
    
    # TC 2: 자산 30억, 배우자 있음 (10억 공제) -> 과표 20억
    # 10억 초과 30억 이하: (20억 * 0.4) - 1.6억 = 8억 - 1.6억 = 6.4억
    res2 = calc.calculate_inheritance_tax(3000000000, 0, True, 2)
    print(f"TC2 (30억): {res2['tax_amount']} (Expect: 640,000,000)")
    assert res2['tax_amount'] == 640000000
    
    # TC 3: 자산 100억, 배우자 없음 (5억 공제) -> 과표 95억
    # 30억 초과: (95억 * 0.5) - 4.6억 = 47.5억 - 4.6억 = 42.9억
    res3 = calc.calculate_inheritance_tax(10000000000, 0, False, 2)
    print(f"TC3 (100억): {res3['tax_amount']} (Expect: 4,290,000,000)")
    assert res3['tax_amount'] == 4290000000

if __name__ == "__main__":
    try:
        test_calc()
        print("\n[SUCCESS] 모든 테스트 케이스 통과!")
    except Exception as e:
        print(f"\n[FAIL] 테스트 실패: {e}")
