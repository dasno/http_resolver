# HTTP Resolver doménových mien
<b> Autor : </b> Daniel Pohančaník (xpohan03@stud.fit.vutbr.cz)

<b>Stručný popis implementácie:</b>
Po spustení server vytvorí socket a aktívne vyčkáva na porte špecifikovanom v argumente pri spustení serveru. Keď dostane správu od klienta tak ju dekóduje a rozparsuje aby z nej dostal potrebné informácie. Server následne vykoná kontrolu správnosti dotazu. Po jej dokončení server preloží doménové meno na adresu alebo adresu na doménové meno podľa typu dotazu. Na preklad sa používa API operačného systému. Po nájdení prekladu server správu upraví to požadovaného formátu, zakóduje a odošle klientovi. Následne server opäť vyčkáva na správu od klienta.

<b>Príklad spustenia</b>:

	
    make run PORT=1234 // Server počúva na porte 1234


