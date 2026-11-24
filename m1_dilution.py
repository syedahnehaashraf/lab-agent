import asyncio
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import LiquidHandlerChatterboxBackend
from pylabrobot.resources.hamilton import STARLetDeck          # check against step 1
from pylabrobot.resources import TIP_CAR_480_A00, PLT_CAR_L5AC_A00, cor_96_wellplate_360uL_Fb  # check
from pylabrobot.resources.hamilton import hamilton_96_tiprack_300uL_filter

TRANSFER_UL = 50   # 50 into 100 = 1-in-3
MIX_UL = 75
MIX_CYCLES = 3

def column(n):
    """All 8 wells (or tips) in column n, e.g. column(3) -> 'A3:H3'."""
    return f"A{n}:H{n}"

async def main():
    lh = LiquidHandler(backend=LiquidHandlerChatterboxBackend(), deck=STARLetDeck())
    await lh.setup()

    tip_car = TIP_CAR_480_A00(name="tip_carrier")
    tip_car[0] = tips = hamilton_96_tiprack_300uL_filter(name="tips")
    lh.deck.assign_child_resource(tip_car, rails=3)

    plate_car = PLT_CAR_L5AC_A00(name="plate_carrier")
    plate_car[0] = plate = cor_96_wellplate_360uL_Fb(name="cr_plate")
    lh.deck.assign_child_resource(plate_car, rails=15)

    # Tip policy: change tips everytime to prevent carry over
    await lh.pick_up_tips(tips[column(1)])

    for n in range(1,11):    
        await lh.aspirate(plate[column(n)], vols=[TRANSFER_UL] * 8)
        await lh.dispense(plate[column(n+1)], vols=[TRANSFER_UL] * 8)

    # TODO 2: loop over source columns 1..10. For each:
    #   - aspirate TRANSFER_UL from column n
    #   - dispense into column n+1
    #   - mix: MIX_CYCLES x (aspirate MIX_UL, dispense MIX_UL) in column n+1
    #   Hint: await lh.aspirate(plate[column(n)], vols=[TRANSFER_UL] * 8)

    # TODO 3: get rid of the tips at the end, then shut down
    await lh.stop()

asyncio.run(main())