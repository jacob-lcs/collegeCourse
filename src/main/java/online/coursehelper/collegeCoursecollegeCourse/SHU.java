package online.coursehelper.collegeCoursecollegeCourse;

import com.alibaba.fastjson.JSONObject;
import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * @author Jacob
 * @Deprecated 自动获取上海大学课表
 * @param {String} 学号
 * @param {String} 密码
 * @return List
 */
public class SHU {
    public static List<JSONObject> getCourse(String number, String psd) {
        List<JSONObject> course = new ArrayList<>();
        try {
            Document doc;
            System.out.println("正在登录.....");
            Connection.Response connect = Jsoup.connect("https://oauth.shu.edu.cn/oauth/authorize?response_type=code&client_id=yRQLJfUsx326fSeKNUCtooKw&redirect_uri=http://cj.shu.edu.cn/passport/return&state=").execute();

            Map<String, String> user_password = new HashMap<String, String>();
            user_password.put("username", number);
            user_password.put("password", psd);
            user_password.put("login_submit", "登录/Login");

            Connection.Response connect1 = Jsoup.connect("https://oauth.shu.edu.cn/login")
                    .data(user_password)
                    .cookies(connect.cookies()).followRedirects(false)
                    .method(Connection.Method.POST).timeout(10000).execute();
            System.out.println(connect1.header("location"));
            Connection.Response connect2 = Jsoup.connect("https://oauth.shu.edu.cn/oauth/authorize")
                    .cookies(connect.cookies()).followRedirects(false)
                    .method(Connection.Method.GET).timeout(10000).execute();
            Connection.Response connect3 = Jsoup.connect(connect2.header("location"))
                    .cookies(connect.cookies()).followRedirects(false)
                    .method(Connection.Method.GET).timeout(10000).execute();
            System.out.println("登录成功！");
            System.out.println("正在获取课表.....");
            doc = Jsoup.connect("http://cj.shu.edu.cn/StudentPortal/StudentSchedule")
                    .data("studentNo", number)
                    .cookies(connect3.cookies())
                    .post();
            Elements term = doc.body().select("option");
            String academicTermID = term.last().attr("value");
            Element coursePage = Jsoup.connect("http://cj.shu.edu.cn/StudentPortal/CtrlStudentSchedule")
                    .data("academicTermID", academicTermID)
                    .cookies(connect3.cookies())
                    .post()
                    .body();
            Elements ele2 = coursePage.select("tr");
            for (int i = 2; i < ele2.size(); i++) {
                JSONObject courseItem = new JSONObject();
                Elements items = ele2.get(i).getElementsByTag("td");
                if(items.size() < 8){
                    continue;
                }
                courseItem.put("课程编号", items.get(0).text());
                courseItem.put("课程名称", items.get(1).text());
                courseItem.put("教师号", items.get(2).text());
                courseItem.put("教师姓名", items.get(3).text());
                courseItem.put("上课时间", items.get(4).text());
                courseItem.put("上课教室", items.get(5).text());
                courseItem.put("答疑时间", items.get(6).text());
                courseItem.put("答疑地点", items.get(7).text());
                course.add(courseItem);
                courseItem = new JSONObject();
            }
            System.out.println("获取成功！");
        } catch (Exception e) {
            e.printStackTrace();
        }
        return course;
    }
}
