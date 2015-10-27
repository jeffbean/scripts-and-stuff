for i in `seq 0 3`; do cat ipmitool | ssh sc9-2$i "cat > ipmitool"; done
for i in `seq 0 3`; do cat libcrypto.so.10 | ssh sc9-2$i "cat > /lib/libcrypto.so.10"; done
for i in `seq 0 3`; do cat libreadline.so.6 | ssh sc9-2$i "cat > /lib/libreadline.so.6"; done



cat ipmitool | ssh scqa1-26 "cat > ipmitool" && cat libcrypto.so.7 | ssh scqa1-26 "cat > /lib/libcrypto.so.7" && cat libreadline.so.5 | ssh scqa1-26 "cat > /lib/libreadline.so.5"

chmod 777 ipmitool && cp ipmitool /usr/sbin/ipmitool && modprobe ipmi_devintf && modprobe ipmi_si 




cat ipmitool | ssh scqa1-29 "cat > ipmitool" && cat libcrypto.so.7 | ssh scqa1-29 "cat > /lib/libcrypto.so.7" && cat libreadline.so.5 | ssh scqa1-29 "cat > /lib/libreadline.so.5"

chmod 777 ipmitool && cp ipmitool /usr/sbin/ipmitool && modprobe ipmi_devintf && modprobe ipmi_si 



cat /lib64/libncurses.so.5 | ssh sc9-20 "cat > /lib64/libncurses.so.5" && cat /lib64/libcrypto.so.10 | ssh sc9-20 "cat > /lib64/libcrypto.so.10"
 

