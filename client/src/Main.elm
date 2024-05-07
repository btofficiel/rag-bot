port module Main exposing (..)

import Browser exposing (Document)
import Html exposing (Html, button, div, img, section, text, textarea)
import Html.Attributes exposing (class, id, placeholder, rows, src, value)
import Html.Events exposing (onClick, onInput)
import Process
import Task



-- MODEL


type alias Model =
    { query : String
    , state : State
    , chat : List Convo
    }


initialModel : Model
initialModel =
    { query = ""
    , state = Rest
    , chat = [ RAG "Hi I am RAG-Man, and I am here to answer your queries about your data using a RAG system. Shoot your questions..." ]
    }



-- UPDATE


type Msg
    = Response String
    | EnterQuery String
    | Ask
    | ChangeState State


type State
    = Rest
    | Loading


type Convo
    = You String
    | RAG String


delay : Msg -> Cmd Msg
delay msg =
    Process.sleep 500
        |> Task.andThen (always <| Task.succeed msg)
        |> Task.perform identity


port askQuery : String -> Cmd msg


port messageReceiver : (String -> msg) -> Sub msg


subscriptions : Model -> Sub Msg
subscriptions _ =
    messageReceiver Response


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        EnterQuery query ->
            ( { model
                | query = query
              }
            , Cmd.none
            )

        Ask ->
            let
                chat =
                    model.chat ++ [ You model.query ]
            in
            ( { model
                | chat = chat
                , query = ""
              }
            , Cmd.batch [ delay (ChangeState Loading), askQuery model.query ]
            )

        ChangeState state ->
            ( { model
                | state = state
              }
            , Cmd.none
            )

        Response resp ->
            let
                chat =
                    model.chat ++ [ RAG resp ]
            in
            ( { model
                | chat = chat
                , state = Rest
              }
            , Cmd.none
            )



-- VIEW


rag : String -> Html Msg
rag msg =
    div [ class "message" ]
        [ img [ src "public/img/bot.jpeg", class "avatar" ] []
        , div [ class "name" ] [ text "RAG-Man" ]
        , div [ class "text" ]
            [ text msg ]
        ]


loading : Html Msg
loading =
    div [ class "message" ]
        [ img [ src "public/img/bot.jpeg", class "avatar" ] []
        , div [ class "name" ] [ text "RAG-Man" ]
        , div [ class "typing-loader" ] []
        ]


you : String -> Html Msg
you msg =
    div [ class "message" ]
        [ img [ src "public/img/human.jpg", class "avatar" ] []
        , div [ class "name" ] [ text "You" ]
        , div [ class "text" ]
            [ text msg ]
        ]


content : Model -> List (Html Msg)
content model =
    [ section [ id "content" ]
        [ div [ id "chat" ]
            (List.map
                (\chat ->
                    case chat of
                        RAG str ->
                            rag str

                        You str ->
                            you str
                )
                model.chat
                ++ (case model.state of
                        Rest ->
                            []

                        Loading ->
                            [ loading ]
                   )
            )
        , div [ id "actions" ]
            [ div [ class "textbox" ]
                [ textarea [ rows 2, placeholder "Write your query...", onInput EnterQuery, value model.query ] []
                ]
            , div [ class "button", onClick Ask ] [ text "Ask" ]
            ]
        ]
    ]


view : Model -> Document Msg
view model =
    { title = "RAG-Man"
    , body = content model
    }



-- MAIN


main : Program () Model Msg
main =
    Browser.document
        { init = \_ -> ( initialModel, Cmd.none )
        , update = update
        , view = view
        , subscriptions = subscriptions
        }
