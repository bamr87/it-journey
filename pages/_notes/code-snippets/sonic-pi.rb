# Welcome to Sonic Pi

## Cadence Chrods C-Major

live_loop :foo do
  use_synth :piano
  play chord(:C4, :major)
  sleep 0.5
  play chord(:F4, :major)
  sleep 0.5
  play chord(:C4, :major)
  sleep 0.5
  play chord(:G3, :major)
  sleep 0.5
  play chord(:G3, :dim7)
  sleep 0.5
  play chord(:c4, :major)
  sleep 1
  
end
