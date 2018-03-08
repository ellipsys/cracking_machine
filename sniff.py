#!/bin/bash
clear
DUMP_PATH="/tmp/TMPlinset"
DEAUTHTIME="8"
IP=192.168.1.1
RANG_IP=$(echo $IP | cut -d "." -f 1,2,3)

#Colores
blanco="\033[1;37m"
gris="\033[0;37m"
magenta="\033[0;35m"
rojo="\033[1;31m"
verde="\033[1;32m"
amarillo="\033[1;33m"
azul="\033[1;34m"
rescolor="\e[0m"
function exitmode {
	
	echo -e "\n\n"$blanco"["$rojo" "$blanco"] "$rojo"Ejecutando la limpieza y cerrando."$rescolor""
	
	if ps -A | grep -q aireplay-ng; then
		echo -e ""$blanco"["$rojo"-"$blanco"] "$blanco"Matando "$gris"aireplay-ng"$rescolor""
		killall aireplay-ng &>$linset_output_device
	fi
	
	if ps -A | grep -q airodump-ng; then
		echo -e ""$blanco"["$rojo"-"$blanco"] "$blanco"Matando "$gris"airodump-ng"$rescolor""
		killall airodump-ng &>$linset_output_device
	fi
	
	if ps a | grep python| grep fakedns; then
		echo -e ""$blanco"["$rojo"-"$blanco"] "$blanco"Matando "$gris"python"$rescolor""
		kill $(ps a | grep python| grep fakedns | awk '{print $1}') &>$linset_output_device
	fi
	
	if ps -A | grep -q hostapd; then
		echo -e ""$blanco"["$rojo"-"$blanco"] "$blanco"Matando "$gris"hostapd"$rescolor""
		killall hostapd &>$linset_output_device
	fi
	 
	if ps -A | grep -q lighttpd; then
		echo -e ""$blanco"["$rojo"-"$blanco"] "$blanco"Matando "$gris"lighttpd"$rescolor""
		killall lighttpd &>$linset_output_device
	fi
	 
	if ps -A | grep -q dhcpd; then
		echo -e ""$blanco"["$rojo"-"$blanco"] "$blanco"Matando "$gris"dhcpd"$rescolor""
		killall dhcpd &>$linset_output_device
	fi
	
	if ps -A | grep -q mdk3; then
		echo -e ""$blanco"["$rojo"-"$blanco"] "$blanco"Matando "$gris"mdk3"$rescolor""
		killall mdk3 &>$linset_output_device
	fi
	
	if [ "$WIFI_MONITOR" != "" ]; then
		echo -e ""$blanco"["$rojo"-"$blanco"] "$blanco"Deteniendo interface "$verde"$WIFI_MONITOR"$rescolor""
		airmon-ng stop $WIFI_MONITOR &> $linset_output_device
	fi
	
	if [ "$WIFI" != "" ]; then
		echo -e ""$blanco"["$rojo"-"$blanco"] "$blanco"Deteniendo interface "$verde"$WIFI"$rescolor""
		airmon-ng stop $WIFI &> $linset_output_device
	fi
	
	if [ "$(cat /proc/sys/net/ipv4/ip_forward)" != "0" ]; then
		echo -e ""$blanco"["$rojo"-"$blanco"] "$blanco"Restaurando "$gris"ipforwarding"$rescolor""
		echo "0" > /proc/sys/net/ipv4/ip_forward #stop ipforwarding
	fi
	
	echo -e ""$blanco"["$rojo"-"$blanco"] "$blanco"Limpiando "$gris"iptables"$rescolor""
	iptables --flush
	iptables --table nat --flush
	iptables --delete-chain
	iptables --table nat --delete-chain
	
	echo -e ""$blanco"["$rojo"-"$blanco"] "$blanco"Restaurando "$gris"tput"$rescolor""
	tput cnorm
	
	if [ $LINSET_DEBUG != 1 ]; then
		
		echo -e ""$blanco"["$rojo"-"$blanco"] "$blanco"Eliminando "$gris"archivos"$rescolor""
		rm -R $DUMP_PATH/* &>$linset_output_device
	fi
	
	echo -e ""$blanco"["$rojo"-"$blanco"] "$blanco"Reiniciando "$gris"NetworkManager"$rescolor""
	service restart networkmanager &> $linset_output_device &
	
	echo -e ""$blanco"["$verde"+"$blanco"] "$verde"Limpiza efectuada con exito!"$rescolor""
	exit
	
}

DIALOG_WEB_INFO_ESP="Por razones de seguridad, introduzca la contrase&ntilde;a <b>"$Host_ENC"</b> para acceder a Internet"
DIALOG_WEB_INPUT_ESP="Introduzca su contrase&ntilde;a WPA:"
DIALOG_WEB_SUBMIT_ESP="Enviar"
DIALOG_WEB_ERROR_ESP="<b><font color=\"red\" size=\"3\">Error</font>:</b> La contrase&ntilde;a introducida <b>NO</b> es correcta!</b>"
DIALOG_WEB_OK_ESP="Su conexi&oacute;n se restablecer&aacute; en breves momentos."
DIALOG_WEB_BACK_ESP="Atr&aacute;s"
DIALOG_WEB_LENGHT_MIN_ESP="La clave debe ser superior a 7 caracteres"

DIALOG_WEB_LENGHT_MAX_ESP="La clave debe ser inferior a 64 caracteres"
