package online.coursehelper.collegeCoursecollegeCourse;
import com.alibaba.fastjson.JSONObject;

import java.util.List;
import java.util.Scanner;

public class App {

    public static void main(String[] args) {
//        Scanner sc = new Scanner(System.in);
//        System.out.println("请输入你的学号：");
//        String name = sc.nextLine();
//        System.out.println("请输入你的密码：");
//        String psd = sc.nextLine();
        String name = "2016210214";
        String psd = "q1w2e3r4";
        // 上海大学
        // List<JSONObject> res = SHU.getCourse(name, psd);

        //青岛大学
        QU.getCourse(name, psd);
//        System.out.println(res);
    }
}
