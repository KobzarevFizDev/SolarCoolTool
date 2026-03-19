using System.Threading.Tasks;
using Cake.Core;
using Cake.Core.Diagnostics;
using Cake.Frosting;

public static class Program
{
    public static int Main(string[] args)
    {
        return new CakeHost()
            .UseContext<BuildContext>()
            .Run(args);
    }
}


public class BuildContext : FrostingContext
{
    public bool Delay { get; set; }

    public BuildContext(ICakeContext context)
        : base(context)
    {
        Delay = context.Arguments.HasArgument("delay");
        context.Arguments.GetArgument("platform");
    }
}

[TaskName("Build")]
public sealed class BuildTask : FrostingTask<BuildContext>
{
    public override void Run(BuildContext context)
    {
        base.Run(context);
    }
}

// [TaskName("Hello")]
// public sealed class HelloTask : FrostingTask<BuildContext>
// {
//     public override void Run(BuildContext context)
//     {
//         context.Log.Information("Hello");
//     }
// }

// [TaskName("World")]
// [IsDependentOn(typeof(HelloTask))]
// public sealed class WorldTask : AsyncFrostingTask<BuildContext>
// {
//     // Tasks can be asynchronous
//     public override async Task RunAsync(BuildContext context)
//     {
//         if (context.Delay)
//         {
//             context.Log.Information("Waiting...");
//             await Task.Delay(1500);
//         }

//         context.Log.Information("World");
//     }
// }

[TaskName("Default")]
public class DefaultTask : FrostingTask
{
    public override void Run(ICakeContext context)
    {
        base.Run(context);
    }
}