# .NET Setup{How to build the BaSyx .NET Core SDK}

The BaSyx .NET Core SDK can be build via dotnet CLI as wells as Microsoft Visual Studio. It uses NuGet for dependency management. This article will detail on how to build the .NET Core SDK from a fresh checkout.

## Requirements
The BaSyx .NET Core SDK requires the following dependencies to successfully build:

* .NET Core SDK 2.2 [Download](https://dotnet.microsoft.com/en-us/download/dotnet/2.2)
* (Optional but really helpful) Microsoft Visual Studio >=2017 Community Edition [Download](https://visualstudio.microsoft.com/de/vs/community/)

## Getting started
1. Create a folder somewhere on your drive and open CommandLine/PowerShell/Terminal in it
2. Clone BaSyx Repository: git clone https://git.eclipse.org/r/basyx/basyx
3. Navigate to folder {your-folder}/sdks/dotnet/
4. Open BaSyx.SDK.sln in Visual Studio
5. Build -> Rebuild Solution
6. Done!

Note: Having built the project, in the respective build folder (bin) of each project NuGet Packages have been generated. This is the recommended way of using BaSys libraries within other projects. It is highly recommended to put all Nuget Packages into one folder and consider it as Local repository. To add a Local Repository, in Visual Studio go:

1. Tools -> Options -> NuGet Package Manager -> Package Sources
2. Press green "+" to add your local repository, give it a name and choose location by pressing "..."
3. Press "Update" and "OK"
4. Now you can select your local repository as NuGet Package source when adding new libraries to your project via NuGet Package Manager

## Hello World Example

To get your first Asset Administation Shell up and running, do the following;

1. In Solution Explorer expand "Examples" folder
2. Right-click on HelloAssetAdministationShell-Project
3. Select "Set as StartUp Project"
4. Press Play!
5. Open your favorite browser and enter: "http://localhost:5080/ui"
6. Now you should see a graphical user interface of the HelloAssetAdministrationShell