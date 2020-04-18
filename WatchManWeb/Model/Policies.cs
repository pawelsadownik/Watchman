using Microsoft.AspNetCore.Authorization;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace WatchmanWeb.Model
{
    public class Policies
    {
        public const string Admin = "Admin";
        public const string AdvancedUser = "AdvancedUser";
        public const string BasicUser = "BasicUser";

        public static AuthorizationPolicy AdminPolicy()
        {
            return new AuthorizationPolicyBuilder().RequireAuthenticatedUser().RequireRole(Admin).Build();
        }

        public static AuthorizationPolicy AdvancedUserPolicy()
        {
            return new AuthorizationPolicyBuilder().RequireAuthenticatedUser().RequireRole(AdvancedUser).Build();
        }

        public static AuthorizationPolicy BasicUserPolicy()
        {
            return new AuthorizationPolicyBuilder().RequireAuthenticatedUser().RequireRole(BasicUser).Build();
        }
    }
}
