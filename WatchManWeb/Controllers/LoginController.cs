using System;
using System.Collections.Generic;
using System.IdentityModel.Tokens.Jwt;
using System.Linq;
using System.Security.Claims;
using System.Text;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;
using WatchmanWeb.Model;

namespace WatchmanWeb.Controllers
{
    [Route("api/[controller]")]
    public class LoginController : Controller
    {
        private readonly IConfiguration _config;
        // TO DO:
        // Create DB with users:
        private List<User> appUsers = new List<User>
        {
            new User {  FirstName = "admin",  UserName = "admin", Password = "1234", UserType = "Admin" },
            new User {  FirstName = "advanced",  UserName = "advanced", Password = "1234", UserType = "AdvancedUser" },
            new User {  FirstName = "basic",  UserName = "basic", Password = "1234", UserType = "BasicUser" }
        };

        public LoginController(IConfiguration config)
        {
            _config = config;
        }

        [HttpPost]
        [AllowAnonymous]
        public IActionResult Login([FromBody]User login)
        {
            IActionResult response = Unauthorized();
            User user = AuthenticateUser(login);
            if (user != null)
            {
                var tokenString = GenerateJWT(user);
                response = Ok(new
                {
                    token = tokenString,
                    userDetails = user,
                });
            }
            return response;
        }

        User AuthenticateUser(User loginCredentials)
        {
            User user = appUsers.SingleOrDefault(x => x.UserName == loginCredentials.UserName && x.Password == loginCredentials.Password);
            return user;
        }

        string GenerateJWT(User userInfo)
        {
            var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_config["Jwt:SecretKey"]));
            var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

            var claims = new[]
            {
                new Claim(JwtRegisteredClaimNames.Sub, userInfo.UserName),
                new Claim("firstName", userInfo.FirstName.ToString()),
                new Claim("role",userInfo.UserType),
                new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
            };

            var token = new JwtSecurityToken(
                issuer: _config["Jwt:Issuer"],
                audience: _config["Jwt:Audience"],
                claims: claims,
                expires: DateTime.Now.AddMinutes(30),
                signingCredentials: credentials
            );
            return new JwtSecurityTokenHandler().WriteToken(token);
        }
    }
}
