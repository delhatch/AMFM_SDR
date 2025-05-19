# AMFM_SDR
Stand-alone radio based on an SDR. No PC required.

![Image](https://github.com/delhatch/AMFM_SDR/blob/main/pictures/topImageSmall.png)
<p>See https://hackaday.io/project/203142-standalone-sdr-fm-am-radio for more information.</p>
<p>Video at https://youtu.be/_GsoaWkBbbo</p>
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
                <p>Main screen showing RF signal at top. Lower portion is a waterfall of the post-IF signal.</p>
            </td>
            <td align="center">
                <img src="https://github.com/delhatch/AMFM_SDR/blob/main/pictures/screen2.jpg" alt="Image 2" height="350">
                <p>Shows full baseband audio (L+R,Pilot,L-R,RDS). Lower portion is L vs. R AudioScope</p>
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="https://github.com/delhatch/AMFM_SDR/blob/main/pictures/screenAM.jpg" alt="Image 3" height="350">
                <p>AM radio screen</p>
            </td>
            <td align="center">
                <img src="https://github.com/delhatch/AMFM_SDR/blob/main/pictures/screenMono.jpg" alt="Image 4" height="350">
                <p>An FM station broadcasting a Mono audio signal. (With the stereo pilot signal on.)</p>
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="https://github.com/delhatch/AMFM_SDR/blob/main/pictures/guts1.jpg" alt="Image 5" height="350">
                <p>I'm not proud of this.</p>
            </td>
            <td align="center">
                <img src="https://github.com/delhatch/AMFM_SDR/blob/main/pictures/guts2.jpg" alt="Image 6" height="350">
                <p>Nope.</p>
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="https://github.com/delhatch/AMFM_SDR/blob/main/pictures/stack1.jpg" alt="Image 7" height="350">
                <p>Rasp Pi 5 at bottom, then custom interface board above that (with green phoenix connectors), with Pi-DAC+ board on top.</p>
            </td>
            <td align="center">
                <img src="https://github.com/delhatch/AMFM_SDR/blob/main/pictures/stack2.jpg" alt="Image 8" height="350">
                <p>Another view of the stack.</p>
            </td>
        </tr>
          <tr>
            <td align="center">
                <img src="https://github.com/delhatch/AMFM_SDR/blob/main/pictures/SDR_tuner.jpg" alt="Image 9" height="350">
                <p>This SDR tuner, receiving a 1kHz tone from a reference broadcast signal. Very low harmonic distortion, but "grassy" noise floor because of the digital signal processing.</p>
            </td>
            <td align="center">
                <img src="https://github.com/delhatch/AMFM_SDR/blob/main/pictures/HighQuality_FM_tuner.jpg" alt="Image 10" height="350">
                <p>High-quality analog FM tuner, receiving a 1kHz tone from a reference broadcast signal. Higher harmonic distortion because of an analog circuit doing the FM demodulation, but with a quiet noise floor.</p>
            </td>
        </tr>
    </table>
