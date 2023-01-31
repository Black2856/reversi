import reversi_system as rs
import sys

op = rs.Option()
op.size = 8
op.start_player = 1
op.frame_rate = 60
op.title = "リバーシ"
op.screen_size = (640,640)

reversi = rs.Reversi_system(op)
reversi.main()