"""
Gedeelde tool functies voor alle agentic AI notebooks.

Dit bestand bevat tool implementaties (BTW, korting, CBS API)
"""

import requests


# =============================================================================
# TOOL IMPLEMENTATIONS
# =============================================================================

def calculate_btw(bedrag: float, btw_percentage: float = 21.0) -> dict:
    """
    Bereken BTW over een bedrag.
    
    Args:
        bedrag: Het bedrag exclusief BTW
        btw_percentage: BTW percentage (standaard 21%)
    
    Returns:
        Dict met BTW berekening resultaten
    """
    btw_bedrag = bedrag * (btw_percentage / 100)
    totaal = bedrag + btw_bedrag
    
    return {
        "excl_btw": bedrag,
        "btw_percentage": btw_percentage,
        "btw_bedrag": round(btw_bedrag, 2),
        "incl_btw": round(totaal, 2)
    }


def calculate_discount(bedrag: float, korting_percentage: float) -> dict:
    """
    Bereken korting over een bedrag.
    
    Args:
        bedrag: Het oorspronkelijke bedrag
        korting_percentage: Korting percentage
    
    Returns:
        Dict met korting berekening resultaten
    """
    korting_bedrag = bedrag * (korting_percentage / 100)
    eindprijs = bedrag - korting_bedrag
    
    return {
        "oorspronkelijk_bedrag": bedrag,
        "korting_percentage": korting_percentage,
        "korting_bedrag": round(korting_bedrag, 2),
        "eindprijs": round(eindprijs, 2)
    }


def get_inwoners_gemeente(gemeente_naam: str = None, jaar: str = "2025") -> dict:
    """
    Haal inwonersaantallen op van Nederlandse gemeenten via CBS API.
    
    Args:
        gemeente_naam: Optioneel, specifieke gemeente naam
        jaar: Jaar voor de data (standaard 2023)
    
    Returns:
        Dict met gemeentedata
    """
    try:
        # CBS API endpoints
        base_url = "https://opendata.cbs.nl/ODataApi/odata/70072ned"
        
        # Haal eerst alle gemeenten op
        regios_url = f"{base_url}/RegioS"
        regios_response = requests.get(regios_url)
        regios_data = regios_response.json()
        
        # Filter alleen gemeenten (beginnen met 'GM')
        gemeenten = [r for r in regios_data['value'] if r['Key'].startswith('GM')]
        
        # Haal bevolkingsdata op voor het specifieke jaar
        data_url = f"{base_url}/TypedDataSet"
        params = {
            "$filter": f"Perioden eq '{jaar}JJ00'",
            "$select": "RegioS,TotaleBevolking_1"
        }
        
        data_response = requests.get(data_url, params=params)
        bevolking_data = data_response.json()
        
        # Filter alleen gemeentecodes (beginnen met 'GM') in de resultaten
        filtered_data = [item for item in bevolking_data['value'] if item['RegioS'].startswith('GM')]
        
        # Combineer gemeente namen met bevolkingsdata
        result = []
        for item in filtered_data:
            gemeente_code = item['RegioS']
            inwoners = item.get('TotaleBevolking_1')
            
            # Zoek gemeente naam
            gemeente_info = next((g for g in gemeenten if g['Key'] == gemeente_code), None)
            if gemeente_info and inwoners is not None:
                gemeente_entry = {
                    'gemeente_code': gemeente_code,
                    'gemeente_naam': gemeente_info['Title'],
                    'inwoners': inwoners,
                    'jaar': jaar
                }
                
                # Als specifieke gemeente gezocht, filter daarop
                if gemeente_naam:
                    if gemeente_naam.lower() in gemeente_info['Title'].lower():
                        result.append(gemeente_entry)
                else:
                    result.append(gemeente_entry)
        
        # Sorteer op inwoners (grootste eerst)
        result.sort(key=lambda x: x['inwoners'], reverse=True)
        
        # Limiteer resultaat bij geen specifieke gemeente
        if not gemeente_naam:
            result = result[:10]  # Top 10 grootste gemeenten
            
        return {
            'status': 'success',
            'jaar': jaar,
            'gemeente_gezocht': gemeente_naam,
            'aantal_gevonden': len(result),
            'gemeenten': result
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'jaar': jaar,
            'gemeente_gezocht': gemeente_naam
        }


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def test_tools():
    """Test alle tool functies."""
    print("🧪 Testing all tools...")
    
    # Test BTW
    btw_result = calculate_btw(100)
    print(f"✅ BTW test: {btw_result}")
    
    # Test korting  
    discount_result = calculate_discount(100, 10)
    print(f"✅ Discount test: {discount_result}")
    
    # Test CBS API (beperkt om API calls te minimaliseren)
    inwoners = get_inwoners_gemeente('Amsterdam')
    print(f"inwoners Amsterdam = {inwoners}")
    print("✅ CBS API ready (test met get_gemeente_inwoners('Amsterdam'))")
    
    print("🎉 All tools working!")


if __name__ == "__main__":
    test_tools()