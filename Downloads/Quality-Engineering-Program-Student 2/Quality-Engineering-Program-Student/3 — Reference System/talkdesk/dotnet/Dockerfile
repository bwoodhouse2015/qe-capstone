FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /build
COPY TalkDesk.csproj .
RUN dotnet restore
COPY Program.cs .
RUN dotnet publish -c Release -o /out

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /out .
# The aspnet image already ships a non-root `app` user (UID 1654); creating one
# fails the build. Use the user that is there.
RUN chown -R app /app
USER app
EXPOSE 8080
ENV ASPNETCORE_URLS=http://0.0.0.0:8080
# No curl and no wget in this image, so the healthcheck asks the runtime that is
# already installed. Checking with a tool the image does not have means the
# container never reports healthy and `--wait` hangs until it times out.
HEALTHCHECK --interval=10s --timeout=3s --start-period=30s --retries=6 \
  CMD ["dotnet", "TalkDesk.dll", "--healthcheck"]
ENTRYPOINT ["dotnet","TalkDesk.dll"]
