import sys
import os

# core 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.calc_engine import InheritanceTaxCalculator
from decimal import Decimal

def test_calc_refined():
    calc = InheritanceTaxCalculator()
    
    # TC 1: 금융재산공제 한도 테스트 (1억 미만)
    # 금융자산 5천만 -> 공제 2천만 (2천만~1억 구간 고정)
    res1 = calc._get_financial_deduction(Decimal('50000000'))
    print(f"TC1 (금융 5천만): {res1} (Expect: 20,000,000)")
    assert res1 == 20000000
    
    # TC 2: 금융재산공제 한도 테스트 (한도 2억)
    # 금융자산 20억 -> 20% 이면 4억이지만 한도 2억 적용
    res2 = calc._get_financial_deduction(Decimal('2000000000'))
    print(f"TC2 (금융 20억): {res2} (Expect: 200,000,000)")
    assert res2 == 200000000
    
    # TC 3: 전체 세액 테스트 (업그레이드 버전)
    # 총자산 30억 (부동산 20억, 금융 10억), 부채 0, 배우자 있음
    # 1. 과세가액 = 30억
    # 2. 공제 = 일괄(5억) + 배우자(5억) + 금융공제(10억의 20% = 2억) = 12억
    # 3. 과표 = 30억 - 12억 = 18억
    # 4. 세액 = (18억 * 0.4) - 1.6억 = 7.2억 - 1.6억 = 5.6억
    res3 = calc.calculate_inheritance_tax(3000000000, 0, True, 1000000000)
    print(f"TC3 (30억-금융10억포함): {res3['tax_amount']} (Expect: 560,000,000)")
    assert res3['tax_amount'] == 560000000

if __name__ == "__main__":
    try:
        test_calc_refined()
        print("\n[SUCCESS] 업그레이드 엔진 테스트 통과!")
    except Exception as e:
        print(f"\n[FAIL] 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
