
#source https://github.com/pymmcore-plus/useq-schema
from pymmcore_plus import CMMCorePlus
from useq import MDASequence

mda_seq = MDASequence(
    time_plan={'interval': 1, 'loops': 20},
    z_plan={"range": 4, "step": 0.5},
    axis_order='tpcz',
)
events = list(mda_seq)

print(len(events))  # 720

print(events[:3])

core = CMMCorePlus()
core.loadSystemConfiguration()  # loads demo by default

core.mda.run(mda_seq)  # run the experiment

# or, construct a sequence of MDAEvents anyway you like
events = [MDAEvent(...), MDAEvent(...), ...]
core.mda.run(events)


