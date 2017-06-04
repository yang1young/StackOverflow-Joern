import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by Qiao Yang on 30/12/2016.
 */
public class RegexUtils {

    //clean code
    public static String codeClean(String input) {
        String pattern = "<code>[^>]+</code>";
        Pattern r = Pattern.compile(pattern);
        Matcher m = r.matcher(input);
        String result = null;
        boolean firstResult = true;

        while (m.find()) {
            if (firstResult) {
                result = m.group();
                firstResult = false;
            } else {
                if (m.group().length() > result.length()) {
                    result = m.group();
                }
            }
        }
        if (result != null && getCodeLongEnough(result)) {
            result = result.replaceAll("&#xA", "\n");
            result = result.replaceAll(";", "");
            result = result.replaceAll("'", "");
            result = result.replaceAll("<[^>]+>", "");
            result = result.replaceAll("&lt", "<");
            result = result.replaceAll("&gt", ">");
            result = result.replaceAll("&amp", "&");
            result = result.replaceAll(" +", " ");
            result = result.replaceAll("[\\r\\n]+", "\n");
            return result;
        }
        return null;
    }

    //to know whether the code is long enough
    public static boolean getCodeLongEnough(String txt) {
        Pattern p = Pattern.compile("&#xA", Pattern.CASE_INSENSITIVE);
        Matcher m = p.matcher(txt);
        int count = 0;
        while (m.find()) {
            count++;
            if (count > 4) {
                return true;
            }
        }
        return false;
    }

    //clean tags
    public static String tagsClean(String tags) {
        String result = tags.replaceAll("><", "#");
        result = result.replaceAll("<", "");
        result = result.replaceAll(">", "");
        return result;
    }

}
