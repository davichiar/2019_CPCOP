package Login;

import com.android.volley.Response;
import com.android.volley.toolbox.StringRequest;

import java.util.Map;

public class LoginCheck extends StringRequest {

    final static private String URL = "http://davichiar1.cafe24.com/MV_LoginCheck.php";
    private Map<String, String> parameters;

    public LoginCheck(Response.Listener<String> listener) {
        super(Method.POST, URL, listener, null);
    }
}
