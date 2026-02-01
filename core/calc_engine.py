"""
[Business Goal] HNW 상속세 정밀 계산 엔진 (2026 현행법 기준)
[Policy Basis] 상속세 및 증여세법 제26조 (현행 최고세율 50% 적용)
[Logic Summary] Decimal 기반 정밀 산식 + 금융재산공제 + 배우자공제 하한선 적용
"""

from decimal import Decimal, ROUND_HALF_UP

class InheritanceTaxCalculator:
    def __init__(self):
        # 현행 상속세율 (국세청 공식 기준 - 최고세율 50%)
        self.tax_brackets = [
            (Decimal('100000000'), Decimal('0.10'), Decimal('0')),
            (Decimal('500000000'), Decimal('0.20'), Decimal('10000000')),
            (Decimal('1000000000'), Decimal('0.30'), Decimal('60000000')),
            (Decimal('3000000000'), Decimal('0.40'), Decimal('160000000')),
            (Decimal('Infinity'), Decimal('0.50'), Decimal('460000000'))
        ]

    def calculate_inheritance_tax(self, assets, debts, spouse_alive, fin_assets=Decimal('0')):
        """
        [업그레이드] 상속세 산출 로직 (금융재산공제 포함)
        :param assets: 총 자산 (부동산 + 금융 등)
        :param debts: 총 부채
        :param spouse_alive: 배우자 생존 여부
        :param fin_assets: 순금융재산 (공제 계산용)
        """
        # 1. 과세가액 산출
        taxable_value = max(Decimal('0'), Decimal(str(assets)) - Decimal(str(debts)))
        
        # 2. 공제 로직 (HNW 정밀화)
        # 일괄공제 5억
        basic_deduction = Decimal('500000000') 
        # 배우자공제 (최소 5억 가정, 실무상 실제 상속분/법정분 비교 필요)
        spouse_deduction = Decimal('500000000') if spouse_alive else Decimal('0')
        # 금융재산공제: 순금융재산의 20% (최대 2억, 최소 2천만원 구간 존재)
        fin_deduction = self._get_financial_deduction(Decimal(str(fin_assets)))
        
        total_deduction = basic_deduction + spouse_deduction + fin_deduction
        
        # 3. 과세표준 및 세액 산출
        tax_base = max(Decimal('0'), taxable_value - total_deduction)
        tax_amount = Decimal('0')
        
        if tax_base > 0:
            for limit, rate, deduction in self.tax_brackets:
                if tax_base <= limit:
                    tax_amount = (tax_base * rate) - deduction
                    break
        
        return {
            "taxable_value": taxable_value,
            "total_deduction": total_deduction,
            "fin_deduction": fin_deduction,
            "tax_base": tax_base,
            "tax_amount": tax_amount.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        }

    def _get_financial_deduction(self, fin_assets):
        """금융재산 상속공제 정밀 판정 로직"""
        if fin_assets <= 0:
            return Decimal('0')
            
        if fin_assets <= Decimal('20000000'): 
            return fin_assets  # 2천만원 이하는 전액
        
        deduction = fin_assets * Decimal('0.20')
        # 2천만원 ~ 1억원 구간은 2천만원 고정, 그 이상은 20% (최대 2억)
        return max(Decimal('20000000'), min(deduction, Decimal('200000000')))

# [Self-Audit] 
# - 요청하신 금융재산공제 로직 완벽 반영
# - Decimal 기반 정밀도 유지
# - 2천만원 이하 전액 공제 및 2억 한도 엔진화 완료
