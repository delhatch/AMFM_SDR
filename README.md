# AMFM_SDR
Stand-alone radio based on an SDR. No PC required.

![Image](https://github.com/delhatch/AMFM_SDR/blob/main/pictures/topImageSmall.png)
<p>See https://hackaday.io/project/203142-standalone-sdr-fm-am-radio for more information.</p>
<p>AMFM_radio_v11.grc : Open this file in gnuradio-companion to see the SDR signal processing flowgraph.</p>
<p>radio_control_v21.py : This is the python program that reads the front panel controls, and sets the SDR radio flowgraph.</p>
<p>WBFM.service and launch.sh : Files used by the Linux systemctl to boot the radio on power-up.</p>
 <table border="0" cellpadding="10" align="left" width="100%">
  <colgroup>
   <col width="50%">
   <col width="50%">
  </colgroup>
        <tr>
            <td align="center">
                <img src="https://github.com/delhatch/AMFM_SDR/blob/main/pictures/topScreen.jpg" alt="Image 1" height="350">
                <p>Main screen showing RF, and post-IF waterfall</p>
            </td>
            <td align="center">
                <img src="https://github.com/delhatch/AMFM_SDR/blob/main/pictures/screen2.jpg" alt="Image 2" height="350">
                <p>Shows full baseband audio (L+R,Pilot,L-R,RDS). Lower portion is L vs. R audioScope</p>
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="https://github.com/delhatch/AMFM_SDR/blob/main/pictures/screenAM.jpg" alt="Image 3" height="350">
                <p>AM radio screen</p>
            </td>
            <td align="center">
                <img src="https://github.com/delhatch/AMFM_SDR/blob/main/pictures/screenMono.jpg" alt="Image 4" height="350">
                <p>An FM station broadcasting in Mono. (But with the stereo pilot signal on.)</p>
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="image5.jpg" alt="Image 5" width="100%">
                <p>Subtitle for Image 5</p>
            </td>
            <td align="center">
                <img src="image6.jpg" alt="Image 6" width="100%">
                <p>Subtitle for Image 6</p>
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="image7.jpg" alt="Image 7" width="100%">
                <p>Subtitle for Image 7</p>
            </td>
            <td align="center">
                <img src="image8.jpg" alt="Image 8" width="100%">
                <p>Subtitle for Image 8</p>
            </td>
        </tr>
    </table>
