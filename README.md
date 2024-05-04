#Esay Mips
راهنما نصب :
برای اجرای برنامه در صورت نصب نبودن پایتون آنرو روی سیستم خودتون نصب کنید ، کتابخانه های مورد نیاز را از فایل requirements نصب کنید ،

دو فایل ui و mips-main رو دانلود و در کنار هم در یک محل قرار بدید ، فایل ui رو اجرا و از برنامه استفاده کنید


راهنمای استفاده:

کد های mips را با فرمت زیر داخل یک فایل تکست بنویسید سپس آدرس فایل رو به برنامه بدید . 
برای مقدار دهی متغیر های به صورت پیش فرض
(توجه شود که نام متغیر باید کوچک باشد)
$s0,...$s7 & $t0,...$t7
دقیقا بصورت زیر عمل میکنید
$s1=12
برای ساخت ارایه ها به این صورت عمل کنید
array $s2
(نمی توان عناصر ارایه را به صورت پیش فرض مقدار دهی کرد و 
باید در طول برنامه انجام شود)

برای اعلام پایان مقدار دهی پیش فرض باید اعلام کنید
end_set
(با حروف کوچک)

سپس میتوانید کد های خود را بصورت یک دستور در هر خط بنویسید
مثال برنامه برای محاسبه حاصل ضرب دو عدد 
(در اینجا $s1 * $s2 = $s3)


$s1 = 8 

$s2 = 7

$s3 = 0

$f = 34

end_set

loop:

beq $s2,$zero,end

add $s3,$s3,$s1

addi $s2,$s2,-1

j loop

end:
