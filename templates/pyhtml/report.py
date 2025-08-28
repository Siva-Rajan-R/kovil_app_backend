from pydantic import EmailStr

def not_found():
    return """
    <body style="min-height: 100vh; display: flex; justify-content: center; align-items: center; background:linear-gradient(to bottom, #fff7e6, #ffe4b3); margin: 0;">
        <div style="background-color: #ff4c4c; padding: 30px; border-radius: 8px; text-align: center; max-width: 400px;">
            <h1 style="color: white; font-size: 24px;">Error 404</h1>
            <p style="color: white; font-size: 16px; margin-top: 10px;">Page Not Found or Request Timed Out</p>
        </div>
    </body>
    """

def register_accept_greet(name:str,email:EmailStr,number:str,role:str):
    return f"""
            <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Registration Success</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen flex items-center justify-center bg-gradient-to-b from-yellow-50 via-orange-50 to-yellow-100 p-4">

  <div class="bg-gradient-to-br from-yellow-200 via-orange-200 to-yellow-300 max-w-lg w-full rounded-2xl shadow-2xl p-10 text-center relative">
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-extrabold text-yellow-900 text-center">Guruvudhasaan</h1>
    </div>

    <!-- Animated Checkmark -->
    <div class="w-20 h-20 mx-auto mb-8 flex items-center justify-center rounded-full bg-green-500 animate-pulse">
      <svg class="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 24 24">
        <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
      </svg>
    </div>

    <!-- Success Message -->
    <h2 class="text-3xl font-extrabold text-yellow-900 mb-4">
      Registration Accepted Successfully!
    </h2>

    <!-- Details -->
    <div class="text-yellow-800 text-lg mb-8">
      <p class="mb-4">You have approved the registration for:</p>
      <div class="bg-yellow-50 rounded-xl p-5 shadow-inner space-y-3">
        <div class="flex justify-between">
          <span class="font-semibold text-orange-700">Name:</span>
          <span class="font-bold text-yellow-900">{name}</span>
        </div>
        <div class="flex justify-between">
          <span class="font-semibold text-orange-700">Email:</span>
          <span class="font-bold text-yellow-900">{email}</span>
        </div>
        <div class="flex justify-between">
          <span class="font-semibold text-orange-700">Mobile Number:</span>
          <span class="font-bold text-yellow-900">{number}</span>
        </div>
        <div class="flex justify-between">
          <span class="font-semibold text-orange-700">Role:</span>
          <span class="font-bold text-yellow-900">{role}</span>
        </div>
      </div>
    </div>

    <!-- Optional Button -->
    <a href="/" class="inline-block bg-orange-600 hover:bg-orange-500 text-white font-bold px-6 py-3 rounded-lg transition">
      Go to Dashboard
    </a>

  </div>

</body>
</html>

    """

def forgot_accept_greet(email_or_no:EmailStr|str):
    return f"""
            <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Forgot Credentials Approved</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-b from-purple-900 via-purple-800 to-purple-700 flex items-center justify-center min-h-screen font-sans">

  <div class="bg-gradient-to-tr from-yellow-400 to-orange-500 max-w-md w-full rounded-2xl p-10 text-center shadow-2xl shadow-purple-800/50 relative overflow-hidden">
    
    <!-- Glowing Animated Circle -->
    <div class="absolute -top-16 -right-16 w-40 h-40 bg-yellow-200 rounded-full opacity-30 animate-pulse"></div>
    <div class="absolute -bottom-16 -left-16 w-40 h-40 bg-orange-400 rounded-full opacity-30 animate-pulse"></div>

    <!-- Checkmark -->
    <div class="w-20 h-20 bg-white rounded-full mx-auto flex items-center justify-center mb-8 shadow-lg shadow-purple-800/50">
      <svg class="w-10 h-10 text-green-600" fill="currentColor" viewBox="0 0 24 24">
        <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
      </svg>
    </div>

    <!-- Success Message -->
    <h2 class="text-purple-900 text-3xl font-extrabold mb-4 drop-shadow-lg">
      Credentials Approved!
    </h2>

    <!-- User Info -->
    <div class="text-purple-900 text-lg leading-relaxed mb-8">
      <p class="mb-3">The forgot credentials request has been approved for:</p>
      <div class="bg-white rounded-xl p-4 shadow-inner shadow-purple-600/30">
        <div class="mb-2 flex justify-between">
          <span class="font-semibold text-purple-800">Email or Mobile Number:</span>
          <strong class="text-purple-900">{email_or_no}</strong>
        </div>
      </div>
    </div>

    <!-- Footer / Note -->
    <p class="text-white text-sm mt-4 font-medium">
      🙏 Thank you for trusting <span class="font-bold">Guruvudhasaan</span> services. Stay blessed and connected!
    </p>

    <!-- Optional Action Button -->
    <a href="#" class="mt-6 inline-block bg-purple-900 text-white font-semibold py-3 px-8 rounded-full shadow-lg hover:bg-purple-800 transition-all duration-300">
      Go to Login
    </a>

  </div>
</body>
</html>


    """
