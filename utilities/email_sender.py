import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
email =  "anteicodes@gmail.com"#"mhankbarbarotp@gmail.com" 
password = 'Twicenime0&' #"gamtenk.1"  
def kirim_verifikasi(to, link):
    msg = MIMEMultipart()
    msg["Subject"] = "Verification"
    msg["From"] = email
    msg["To"] = to
    html=f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>verification</title>
    </head>
    <body>
        <div class=""><div class="aHl"></div><div id=":np" tabindex="-1"></div><div id=":ne" class="ii gt"><div id=":nd" class="a3s aiL msg-8238556864057784692"><u></u>
            <div style="margin:0;padding:0;background-color:#d9dffa">
            <table bgcolor="#d9dffa" cellpadding="0" cellspacing="0" role="presentation" style="table-layout:fixed;vertical-align:top;min-width:320px;border-spacing:0;border-collapse:collapse;background-color:#d9dffa;width:100%" valign="top" width="100%">
            <tbody>
            <tr style="vertical-align:top" valign="top">
            <td style="word-break:break-word;vertical-align:top" valign="top">
            <div style="background-color:#cfd6f4">
            <div class="m_-8238556864057784692block-grid" style="min-width:320px;max-width:600px;word-wrap:break-word;word-break:break-word;Margin:0 auto;background-color:transparent">
            <div style="border-collapse:collapse;display:table;width:100%;background-color:transparent">
            <div class="m_-8238556864057784692col" style="min-width:320px;max-width:600px;display:table-cell;vertical-align:top;width:600px">
            <div class="m_-8238556864057784692col_cont" style="width:100%!important">

            <div style="border-top:0px solid transparent;border-left:0px solid transparent;border-bottom:0px solid transparent;border-right:0px solid transparent;padding-top:20px;padding-bottom:0px;padding-right:0px;padding-left:0px">
            <div align="center" style="padding-right:0px;padding-left:0px">
            <img align="center" alt="Card Header with Border and Shadow Animated" border="0" src="https://ci6.googleusercontent.com/proxy/WH1P92PdYMrjl2Z27rfWtW8g4BBt8EQUwWESviToDdBT5QVhcRDNWO3oW2Mn1yJZTTM7uqF29-PrJuMLXa4VWut9krIZX0AzZUMpufaWamWQ6ZA39KSr4yzyLXLB6xLjiH82=s0-d-e1-ft#https://d1oco4z2z1fhwp.cloudfront.net/templates/default/3991/animated_header.gif" style="text-decoration:none;height:auto;border:0;width:100%;max-width:600px;display:block" title="Card Header with Border and Shadow Animated" width="600" class="CToWUd">
            
            </div>
            
            </div>
            
            </div>
            </div>
            
            
            </div>
            </div>
            </div>
            <div style="background-image:url('https://ci3.googleusercontent.com/proxy/Fq_umS0esqdu1yAmY4m3-al2hSoopd6Q6i6QVF2GXM26V6bRnS2f4DmJ8SsBk7WXh20Pn-oSfAk7IGYOJgezmAmAYV0eVRdOaOXDMUWLVI_0HbQ1IjFF0ZP2SzxDg-ORdcH5HGQ=s0-d-e1-ft#https://d1oco4z2z1fhwp.cloudfront.net/templates/default/3991/body_background_2.png');background-position:top center;background-repeat:repeat;background-color:#d9dffa">
            <div class="m_-8238556864057784692block-grid" style="min-width:320px;max-width:600px;word-wrap:break-word;word-break:break-word;Margin:0 auto;background-color:transparent">
            <div style="border-collapse:collapse;display:table;width:100%;background-color:transparent">
            
            
            <div class="m_-8238556864057784692col" style="min-width:320px;max-width:600px;display:table-cell;vertical-align:top;width:600px">
            <div class="m_-8238556864057784692col_cont" style="width:100%!important">
            
            <div style="border-top:0px solid transparent;border-left:0px solid transparent;border-bottom:0px solid transparent;border-right:0px solid transparent;padding-top:15px;padding-bottom:15px;padding-right:50px;padding-left:50px">
            
            
            <div style="color:#506bec;font-family:Helvetica Neue,Helvetica,Arial,sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px">
            <div style="font-size:14px;line-height:1.2;color:#506bec;font-family:Helvetica Neue,Helvetica,Arial,sans-serif">
            <p style="margin:0;font-size:14px;line-height:1.2;word-break:break-word;margin-top:0;margin-bottom:0"><strong><span style="font-size:38px">Activation Your Account</span></strong></p>
            </div>
            </div>
            
            
            <div style="color:#40507a;font-family:Helvetica Neue,Helvetica,Arial,sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px">
            <div style="font-size:14px;line-height:1.2;color:#40507a;font-family:Helvetica Neue,Helvetica,Arial,sans-serif">
            <p style="margin:0;font-size:16px;line-height:1.2;word-break:break-word;margin-top:0;margin-bottom:0"><span style="font-size:16px">Hey, we received a request to Activation Your Account.</span></p>
            </div>
            </div>
            
            
            <div style="color:#40507a;font-family:Helvetica Neue,Helvetica,Arial,sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px">
            <div style="font-size:14px;line-height:1.2;color:#40507a;font-family:Helvetica Neue,Helvetica,Arial,sans-serif">
            <p style="margin:0;font-size:16px;line-height:1.2;word-break:break-word;margin-top:0;margin-bottom:0"><span style="font-size:16px">Let???s get you a new one!</span></p>
            </div>
            </div>
            
            <div align="left" style="padding-top:20px;padding-right:10px;padding-bottom:20px;padding-left:10px">
            <a href="{link}" style="text-decoration:none;display:inline-block;color:#ffffff;background-color:#506bec;border-radius:16px;width:auto;width:auto;border-top:0px solid TRANSPARENT;border-right:0px solid TRANSPARENT;border-bottom:0px solid TRANSPARENT;border-left:0px solid TRANSPARENT;padding-top:8px;padding-bottom:8px;font-family:Helvetica Neue,Helvetica,Arial,sans-serif;text-align:center;word-break:keep-all" target="_blank" data-saferedirecturl="{link}"><span style="padding-left:25px;padding-right:20px;font-size:15px;display:inline-block;letter-spacing:normal"><span style="font-size:16px;line-height:2;word-break:break-word"><span style="font-size:15px;line-height:30px"><strong>verification</strong></span></span></span></a>
            
            </div>
            
            <div style="color:#40507a;font-family:Helvetica Neue,Helvetica,Arial,sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px">
            <div style="font-size:14px;line-height:1.2;color:#40507a;font-family:Helvetica Neue,Helvetica,Arial,sans-serif">
            <p style="margin:0;font-size:14px;line-height:1.2;word-break:break-word;margin-top:0;margin-bottom:0"><span style="font-size:14px">Having trouble? <a href="http://www.example.com/" rel="noopener" style="text-decoration:none;color:#40507a" title="@socialaccount" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://www.example.com/&amp;source=gmail&amp;ust=1624776055226000&amp;usg=AFQjCNFUQwZahrcVkVImWQ48t5A1a_rQVA"><strong>@anteicodes</strong></a></span></p>
            </div>
            </div>
            
            
            <div style="color:#40507a;font-family:Helvetica Neue,Helvetica,Arial,sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px">
            <div style="font-size:14px;line-height:1.2;color:#40507a;font-family:Helvetica Neue,Helvetica,Arial,sans-serif">
            <!-- <p style="margin:0;font-size:14px;line-height:1.2;word-break:break-word;margin-top:0;margin-bottom:0">Didn???t request a password reset? You can ignore this message.</p> -->
            </div>
            </div>
            
            
            </div>
            
            </div>
            </div>
            
            
            </div>
            </div>
            </div>
            <div style="background-color:transparent">
            <div class="m_-8238556864057784692block-grid" style="min-width:320px;max-width:600px;word-wrap:break-word;word-break:break-word;Margin:0 auto;background-color:transparent">
            <div style="border-collapse:collapse;display:table;width:100%;background-color:transparent">
            
            
            <div class="m_-8238556864057784692col" style="min-width:320px;max-width:600px;display:table-cell;vertical-align:top;width:600px">
            <div class="m_-8238556864057784692col_cont" style="width:100%!important">
            
            <div style="border-top:0px solid transparent;border-left:0px solid transparent;border-bottom:0px solid transparent;border-right:0px solid transparent;padding-top:0px;padding-bottom:5px;padding-right:0px;padding-left:0px">
            
            <div align="center" style="padding-right:0px;padding-left:0px">
            <img align="center" alt="Card Bottom with Border and Shadow Image" border="0" src="https://ci6.googleusercontent.com/proxy/-Fj3CgQihW5WL7gxafTKgOH6hN-D34XUHKrBzBOC5RkthFAhI8y7pzNxSaEuqNszL_GQGCOBxKitfJuqTyXPFoaIiiUR6kS_AakJvLPjYGbqtzQWIp6PylsjKuje-w=s0-d-e1-ft#https://d1oco4z2z1fhwp.cloudfront.net/templates/default/3991/bottom_img.png" style="text-decoration:none;height:auto;border:0;width:100%;max-width:600px;display:block" title="Card Bottom with Border and Shadow Image" width="600" class="CToWUd">
            
            </div>
            
            </div>
            
            </div>
            </div>
            
            
            </div>
            </div>
            </div>
            <div style="background-color:transparent">
            <div class="m_-8238556864057784692block-grid" style="min-width:320px;max-width:600px;word-wrap:break-word;word-break:break-word;Margin:0 auto;background-color:transparent">
            <div style="border-collapse:collapse;display:table;width:100%;background-color:transparent">
            
            
            <div class="m_-8238556864057784692col" style="min-width:320px;max-width:600px;display:table-cell;vertical-align:top;width:600px">
            <div class="m_-8238556864057784692col_cont" style="width:100%!important">
            
            <div style="border-top:0px solid transparent;border-left:0px solid transparent;border-bottom:0px solid transparent;border-right:0px solid transparent;padding-top:10px;padding-bottom:20px;padding-right:10px;padding-left:10px">
            
            <div align="center" style="padding-right:10px;padding-left:10px">
            
            <div style="font-size:1px;line-height:10px">&nbsp;</div><a href="http://anteiku.codes" style="outline:none" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://anteicku.codes&amp;source=gmail&amp;ust=1624776055226000&amp;usg=AFQjCNFUQwZahrcVkVImWQ48t5A1a_rQVA"><img align="center" alt="Your Logo" border="0" src="https://avatars.githubusercontent.com/u/86209322" style="text-decoration:none;height:auto;border:0;width:100%;max-width:145px;display:block;filter: sepia(100%) hue-rotate(190deg) saturate(500%);mix-blend-mode: multiply;" title="Your Logo" width="145" class="CToWUd"></a>
            <div style="font-size:1px;line-height:10px">&nbsp;</div>
            
            </div>
            <table cellpadding="0" cellspacing="0" role="presentation" style="table-layout:fixed;vertical-align:top;border-spacing:0;border-collapse:collapse" valign="top" width="100%">
            <tbody>
            <tr style="vertical-align:top" valign="top">
            <td style="word-break:break-word;vertical-align:top;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px" valign="top">
            <table align="center" cellpadding="0" cellspacing="0" role="presentation" style="table-layout:fixed;vertical-align:top;border-spacing:0;border-collapse:collapse" valign="top">
            <tbody>
            <tr align="center" style="vertical-align:top;display:inline-block;text-align:center" valign="top">
            <td style="word-break:break-word;vertical-align:top;padding-bottom:0;padding-right:2.5px;padding-left:2.5px" valign="top"><a href="https://www.instagram.com/" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.instagram.com/&amp;source=gmail&amp;ust=1624776055227000&amp;usg=AFQjCNFna6GDsudGP5Lq_C7dTOEEWwgRpA"><img alt="Instagram" height="32" src="https://ci3.googleusercontent.com/proxy/hKPOB05cye5xCEZwINtWhbZj4fF2cRlWc5Ij2QbPaImb3hcDR7A6owUP_xo3ML_2iluIPgHBUZzto7je0iDYhW_PuEdNhS1O5Zj1bgJQi-DpdonwYCyQfeEYcL-Cul9hQQiMMGSc9O9ApZKreS9YcxPDbU69S7NpOVGVCuhlikepAJu034xJP1rx=s0-d-e1-ft#https://d2fi4ri5dhpqd1.cloudfront.net/public/resources/social-networks-icon-sets/t-only-logo-dark-gray/instagram@2x.png" style="text-decoration:none;height:auto;border:0;display:block" title="instagram" width="32" class="CToWUd"></a></td>
            <td style="word-break:break-word;vertical-align:top;padding-bottom:0;padding-right:2.5px;padding-left:2.5px" valign="top"><a href="https://www.twitter.com/" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.twitter.com/&amp;source=gmail&amp;ust=1624776055227000&amp;usg=AFQjCNEGxTg__VaYSx936fOF7MBNQU1KDA"><img alt="Twitter" height="32" src="https://ci4.googleusercontent.com/proxy/8u3BJ6cbjsnNu81tX8sripKUWNp5KrHWG_wN5qGT9Oj4yO8Oev_gFxzPn-Ts2gjepmBMywk4GMU3VIxNuxLvKE1VUEycFDtVKXC53xl4gIVd8HmYdXYxBZhP7nEkymY-Sr_gt650Rccl5y-aklDJ41iSUlG94-XaywtjPhH1JAzlVdYgPDGz5Q=s0-d-e1-ft#https://d2fi4ri5dhpqd1.cloudfront.net/public/resources/social-networks-icon-sets/t-only-logo-dark-gray/twitter@2x.png" style="text-decoration:none;height:auto;border:0;display:block" title="twitter" width="32" class="CToWUd"></a></td>
            </tr>
            </tbody>
            </table>
            </td>
            </tr>
            </tbody>
            </table>
            
            <div style="color:#97a2da;font-family:Helvetica Neue,Helvetica,Arial,sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px">
            <div style="font-size:14px;line-height:1.2;color:#97a2da;font-family:Helvetica Neue,Helvetica,Arial,sans-serif">
            <p style="margin:0;font-size:14px;line-height:1.2;word-break:break-word;text-align:center;margin-top:0;margin-bottom:0">+62 (82125072597)</p>
            </div>
            </div>
            
            
            <div style="color:#97a2da;font-family:Helvetica Neue,Helvetica,Arial,sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px">
            <div style="font-size:14px;line-height:1.2;color:#97a2da;font-family:Helvetica Neue,Helvetica,Arial,sans-serif">
            <p style="margin:0;font-size:14px;line-height:1.2;word-break:break-word;text-align:center;margin-top:0;margin-bottom:0">This link will expire in the next 24 hours.<br>Please feel free to contact us at <a href="mailto:anteicodes@gmail.com" target="_blank">anteicodes@gmail.com</a>. </p>
            </div>
            </div>
            
            
            <div style="color:#97a2da;font-family:Helvetica Neue,Helvetica,Arial,sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px">
            <div style="font-size:14px;line-height:1.2;color:#97a2da;font-family:Helvetica Neue,Helvetica,Arial,sans-serif">
            <p style="margin:0;text-align:center;font-size:12px;line-height:1.2;word-break:break-word;margin-top:0;margin-bottom:0"><span style="font-size:12px">Copyright?? 2021 AnteiCodes</span></p>
    </div>
            </div>
            
            
            </div>
            
            </div>
            </div>
            
            
            </div>
            </div>
            </div>
            
            </td>
            </tr>
            </tbody>
            </table><div class="yj6qo"></div><div class="adL">
            
            </div></div><div class="adL">
            </div></div></div><div id=":nt" class="ii gt" style="display:none"><div id=":nu" class="a3s aiL "></div></div><div class="hi"></div></div>
    </body>
    </html>"""
    msg.attach(MIMEText(html, 'html'))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email, password)
        server.sendmail("no-reply@gmail.com", to, msg.as_string())
        server.quit()
        print(f"terkirim: {to}")
    except Exception as e:
        print(e)

