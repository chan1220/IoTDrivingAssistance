package com.example.kpu.googlelogintest.activitys;

import android.content.Intent;
import android.os.Bundle;
import android.os.StrictMode;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.view.View;

import com.example.kpu.googlelogintest.R;
import com.example.kpu.googlelogintest.utills.PHPRequest;
import com.google.android.gms.auth.api.Auth;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.auth.api.signin.GoogleSignInResult;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.SignInButton;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.firebase.iid.FirebaseInstanceId;

public class LoginActivity extends AppCompatActivity {
    private static final int RESOLVE_CONNECTION_REQUEST_CODE = 1;
    GoogleApiClient mGoogleApiClient;
    SignInButton googleLoginButton;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
//        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
//                WindowManager.LayoutParams.FLAG_FULLSCREEN); // 풀스크린 만들기
        getSupportActionBar().hide(); // 엑션 바 감추기

        setContentView(R.layout.activity_login);

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        googleLoginButton = findViewById(R.id.button_login_google);

        GoogleSignInOptions gso = new GoogleSignInOptions.Builder( GoogleSignInOptions.DEFAULT_SIGN_IN )
                .requestEmail( )
                .requestProfile( )
                .build( );

        mGoogleApiClient = new GoogleApiClient.Builder(LoginActivity.this)
                .enableAutoManage( LoginActivity.this, new GoogleApiClient.OnConnectionFailedListener( )
                {
                    @Override
                    public void onConnectionFailed( @NonNull ConnectionResult connectionResult )
                    {
                        // 연결에 실패했을 경우 실행되는 메서드입니다.
                    }
                } ).addApi( Auth.GOOGLE_SIGN_IN_API, gso ).build( );



        googleLoginButton.setOnClickListener( new View.OnClickListener( )
        {
            @Override public void onClick(View view )
            { // 구글 로그인 화면을 출력합니다. 화면이 닫힌 후 onActivityResult가 실행됩니다.
                Intent signInIntent = Auth.GoogleSignInApi.getSignInIntent( mGoogleApiClient );
                startActivityForResult( signInIntent, RESOLVE_CONNECTION_REQUEST_CODE );
            }
        } );


    }

    @Override
    protected void onActivityResult( int requestCode, int resultCode, Intent data )
    {
        switch ( requestCode )
        {
            case RESOLVE_CONNECTION_REQUEST_CODE:
                GoogleSignInResult result = Auth.GoogleSignInApi.getSignInResultFromIntent(data);
                if ( result.isSuccess( ) )
                {
                    GoogleSignInAccount acct = result.getSignInAccount( ); // 계정 정보 얻어오기
                    String id, name, token;
                    name = acct.getDisplayName();
                    id = acct.getId();
                    token = FirebaseInstanceId.getInstance().getToken();

                    Intent intent=new Intent(LoginActivity.this,MainActivity.class);
                    intent.putExtra("name",name);
                    intent.putExtra("email",acct.getEmail());
                    intent.putExtra("id",id);

                    // 실행!
                    PHPRequest.execute(getString(R.string.server_url)+"/register_user.php","id",id,"name",name,"token",token);
                    startActivity(intent);
                    finish();

                }
                break;

            default:
                super.onActivityResult( requestCode, resultCode, data );
        }
    }




}



