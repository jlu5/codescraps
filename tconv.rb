puts 'Enter amount of seconds:'
t = gets.chomp.to_i
#t = 454544
mm, ss = t.divmod(60)
hh, mm = mm.divmod(60)
dd, hh = hh.divmod(24)
puts "%d days, %d hours, %d minutes and %d seconds" % [dd, hh, mm, ss]
#puts "I have been running for %d days, %d:%d:%d." % [dd, 
#hh.to_s.rjust(2, '0'), mm.to_s.rjust(2, '0'), ss.to_s.rjust(2, '0')]