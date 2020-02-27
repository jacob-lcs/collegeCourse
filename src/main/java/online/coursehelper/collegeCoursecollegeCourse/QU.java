package online.coursehelper.collegeCoursecollegeCourse;

import org.jsoup.Connection;
import org.jsoup.Jsoup;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.io.ByteArrayInputStream;

public class QU {
    public static void getCourse(String number, String psd) {
        try {
            System.out.println("正在登录.....");
            Connection.Response connect = Jsoup.connect("http://jw.qdu.edu.cn/academic/student/currcourse/currcourse.jsdo?year=39&term=2").execute();
            System.out.println(connect.cookies());
            Connection.Response verification_code = Jsoup.connect("http://jw.qdu.edu.cn/academic/getCaptcha.do?0.3851235093964869")
                    .cookies(connect.cookies())
                    .ignoreContentType(true)
                    .execute();
            ImageIcon image = new ImageIcon(ImageIO.read(new ByteArrayInputStream(verification_code.bodyAsBytes())));
            JOptionPane.showMessageDialog(null, image, "Captcha image", JOptionPane.PLAIN_MESSAGE);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
